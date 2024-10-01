# I <3 mom
#TESTING
from random import *
from datetime import datetime, timedelta
from utils import *
import pymongo
#from pymongo import UpdateOne
import psycopg2
import psycopg2.extras
import time
import threading
from multiprocessing import Process, cpu_count


def chunks(lst, n):
    """Yield n successive chunks from lst."""
    if len(lst) > 0:
        chunk_size = -(-len(lst) // n)
        print("chunk_size is: {}".format(chunk_size))
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

def sync_to_live_table(ship_list,tile_status_collection):

    try:
        #create connection  
        conn = None
        if len(ship_list) > 0:
            conn = my_conn()       
            # start dataship
            shipping_count = 0
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # start to ship from temp table to formal table per tile
                    for document in ship_list:                            
                        tile_encoding = document['tile'] if 'tile' in document and document['tile'] else None
                        incumbent_id = document['id'] if 'tile' in document and document['id'] else None
                        if tile_encoding and incumbent_id:
                                                
                            # step 1: shipping grid data from temp table to live table
                            cur.execute("CALL do_griddb_datasync('{}',{},'{}');".format(TB_BASE_NAME, incumbent_id, tile_encoding))
                            conn.commit()
                            drop_statement = "DROP TABLE IF EXISTS {}_{}_{}_temp;".format(TB_BASE_NAME,tile_encoding,incumbent_id)
                            cur.execute(drop_statement)
                            conn.commit()

                            # step 2: update tile status to shipped
                            filter_statement = { 'id': document['id'],'tile': document['tile']}
                            update_statement = { 
                                "$set": { 
                                    'status': SHIPPING_STATUS 
                                },
                                "$currentDate": { "updated_time": { "$type": "timestamp"}}
                             }
                            tile_status_collection.update_one(filter_statement, update_statement)
                            shipping_count += 1
                            if shipping_count % 10 == 0:
                                logger.info("shipping count in grid db is {}".format(shipping_count))

                        else:
                            logger.info("Nothing to be shipped!")

                    cur.close()         
            logger.info("shipping count in grid db is {}".format(shipping_count))
            conn.close()           
        else:
            logger.error("No data to ship!!!!")
           
    except Exception as e:
        logger.error('Error with sync_to_live_table {}'.format(str(e).strip()))
        if conn:
            conn.close()
        raise
                                           
def sync_data_with_multi_threading(ship_list,tile_status_collection,num_thread):
    try:                                                                       
        threads = []
        if len(ship_list) > 0:
            chunk_generator = chunks(ship_list, num_thread)                                                              
            for lst in chunk_generator: 
                                                  
                threads.append(                                                         
                    threading.Thread(target=sync_to_live_table, args=(lst,tile_status_collection)))         
                threads[-1].start() # start the thread we just created                  
                print("start thread {}".format(threads[-1].name))
            # wait for all threads to finish                                            
            for t in threads:                                                           
                t.join()    
    except Exception as e:
        logger.error('sync_data_with_multi_threading {}'.format(str(e).strip()))
        raise


def do_clean_incumbents(base_name, ship_list):
    # start to clean documents from formal table
    try:
        # get new mapping list
        incumbent_id_list = []
        new_incument_mapping = {}
        for each_incumbent in ship_list:
            incumbent_id_list.append(each_incumbent['id'])
            if each_incumbent['id'] not in new_incument_mapping:
                new_incument_mapping[each_incumbent['id']] = []
            new_incument_mapping[each_incumbent['id']].append(each_incumbent['tile'])
        logger.info("incumbent_id_list {} ".format(incumbent_id_list))
        logger.info("new_incument_mapping {}".format(new_incument_mapping))
        # get old mapping from rds
        old_incument_mapping = {}
        if len(incumbent_id_list) > 0:
            conn = my_conn()
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    sql_statement = """
                        SELECT tile_encoding, array_agg(incumbent_id) AS incumbent_id_array
                        FROM tb_incumbent_tile_mapping
                        WHERE incumbent_id IN ({})
                        GROUP BY tile_encoding
                    """.format(','.join("{0}".format(incumbent_id) for incumbent_id in incumbent_id_list))
                    cur.execute(sql_statement)
                    rds_incumbents_mapping = cur.fetchall()
                    for incubment in rds_incumbents_mapping:
                        old_incument_mapping[incubment['tile_encoding']] = incubment['incumbent_id_array']

                    logger.info("old_incument_mapping {} ".format(old_incument_mapping))

                    # key is tile_encoding, value is incumbent id
                    for key, value in old_incument_mapping.items():
                        table_name = base_name + '_' + key
                        print("table_name is {}".format(table_name))
                        # check if table exists
                        checking_statement = """
                            SELECT EXISTS
                                (SELECT 1
                                    FROM   information_schema.tables 
                                    WHERE  table_name = '{}')
                            """.format(table_name)
                        cur.execute(checking_statement)
                        rs = cur.fetchone()
                        
                        if rs['exists']:
                            # in some special cases, there are 12M records to be deleted from one table
                            # initial delete_count, and delete in batch till all deletion is done
                            logger.info("Start to delete records!")
                            delete_count = DEL_CHUNK_SIZE
                            start_time = time.time()
                            while delete_count >= DEL_CHUNK_SIZE:
                                clean_statement_in_batch = """
                                WITH del_rows AS (
                                  WITH batch AS (
                                   SELECT i,t,h               
                                   FROM  {0}
                                   WHERE i IN ({2})
                                   LIMIT  {1}
                                   )
                                DELETE FROM {0} t1
                                USING  batch
                                WHERE t1.i = batch.i
                                AND t1.t = batch.t
                                AND t1.h = batch.h
                                RETURNING *
                                ) 
                                SELECT count(*) AS delete_count FROM del_rows; 
                                """.format(table_name,DEL_CHUNK_SIZE, ','.join("{0}".format(incumbent_id) for incumbent_id in value))
                                cur.execute(clean_statement_in_batch)
                                conn.commit()
                                rs = cur.fetchone()
                                delete_count = rs['delete_count']
                                logger.info("Deleted {} records".format(delete_count))
                                print("--- %s seconds ---" % (time.time() - start_time))
                                start_time = time.time()
                            logger.info("Finish deleting records!")
                        # remove from mapping table tb_incumbent_tile_mapping
                        remove_statement = """
                            DELETE
                            FROM tb_incumbent_tile_mapping
                            WHERE incumbent_id IN ({})
                            AND tile_encoding = '{}'
                            """.format(','.join("{0}".format(incumbent_id) for incumbent_id in value), key)
                        cur.execute(remove_statement)
                    conn.commit()
                    cur.close()

            logger.info("clean incumbents successfully!")

    except Exception as e:
        logger.error('Error with do_clean_incumbents: {}'.format(str(e).strip()))
        raise


def do_data_ship(max_size):

    try:
        # initial mongo client
        mongo_client_incumbent = connect_db_cluster_from_secret(AFC_INCUMBENT_MONGO_URI_SECRET,False)
        logger.info("mongo_client_incumbent connnected!")
        # find out the incumbent_id which is ready to be shipped: all tiles' status are completed for one incumbent
        status_db= mongo_client_incumbent[DB_STATUS_NAME]
        tile_status_collection = status_db[TILE_STATUS_COLLECTION_NAME]
        contour_status_collection = status_db[CONTOUR_STATUS_COLLECTION_NAME]
        # build query
        shipping_count = 0
        find_query = {"id":{"$nin":tile_status_collection.distinct("id",{"status": {"$in": HOLD_STATUS_LIST } })},"status":SUCCESS_STATUS}
        ship_list_origin = list(tile_status_collection.find(find_query))

        if len(ship_list_origin) > 0 and DATA_INITIALIZE == '0':
            ship_list = ship_list_origin[0:max_size]
            # clean existing points data based on ship_list
            do_clean_incumbents(TB_BASE_NAME, ship_list)

            # start dataship
            sync_data_with_multi_threading(ship_list,tile_status_collection, NUM_THREAD)

            # ship incumbent contour data
            incumbent_ids1 = list(set(tile_status_collection.distinct("id",{"status": SHIPPING_STATUS }))-set(contour_status_collection.distinct("id",{"status": SHIPPING_STATUS })))

            incumbent_ids2 = list(set(contour_status_collection.distinct("id",{"status": SUCCESS_STATUS }))-set(tile_status_collection.distinct("id",{})))

            incumbent_ids = incumbent_ids1 + incumbent_ids2


            logger.info("Length of incumbent_ids ready to ship is {}".format(len(incumbent_ids)))
                
            # ship contour data based
            if len(incumbent_ids) > 0:
                # ship contour
                logger.info("Start to ship {} incumbents contour".format(len(incumbent_ids)))
                db_incumbent_temp = mongo_client_incumbent[DB_INCUMBENT_TEMP_NAME]
                db_incumbent_live = mongo_client_incumbent[DB_INCUMBENT_LIVE_NAME]
                collection_incumbent_temp = db_incumbent_temp[INCUMBENT_COLLECTION_NAME]
                collection_incumbent_live = db_incumbent_live[INCUMBENT_COLLECTION_NAME]

                # simplified contour
                simplified_collection_incumbent_temp = db_incumbent_temp[SIMPLIFIED_INCUMBENT_COLLECTION_NAME]
                simplified_collection_incumbent_live = db_incumbent_live[SIMPLIFIED_INCUMBENT_COLLECTION_NAME]

                incumbents_filter = {"incumbent_id":{"$in": list(incumbent_ids)}}

                # ship incumbents to live database
                operations_1 = []
                for doc in collection_incumbent_temp.find(incumbents_filter,{'_id': False}):
                    # Set a random number on every document update
                    operations_1.append(
                        UpdateOne({ "incumbent_id": doc["incumbent_id"] },{'$set': doc}, upsert=True)
                    )

                    # Send once every 1000 in batch
                    if ( len(operations_1) == 1000 ):
                        collection_incumbent_live.bulk_write(operations_1,ordered=False)
                        operations_1 = []

                if ( len(operations_1) > 0 ):
                    collection_incumbent_live.bulk_write(operations_1,ordered=False)

                # ship simplified incumbents to live database
                operations_2 = []
                for doc in simplified_collection_incumbent_temp.find(incumbents_filter,{'_id': False}):
                    # Set a random number on every document update
                    operations_2.append(
                        UpdateOne({ "incumbent_id": doc["incumbent_id"] },{'$set': doc}, upsert=True)
                    )

                    # Send once every 1000 in batch
                    if ( len(operations_2) == 1000 ):
                        simplified_collection_incumbent_live.bulk_write(operations_2,ordered=False)
                        operations_2 = []

                if ( len(operations_2) > 0 ):
                    simplified_collection_incumbent_live.bulk_write(operations_2,ordered=False)

                # update status in contour status collection
                query_contour_status = {"id": {"$in": list(incumbent_ids)}}
                update_contour_status = {"$set": {'status': SHIPPING_STATUS}}
                contour_status_collection.update_many(query_contour_status, update_contour_status)
                logger.info("Successfully shipped {} incumbents contour".format(len(incumbent_ids)))

                # delete those incumbents from temp database
                simplified_collection_incumbent_temp.delete_many(filter = incumbents_filter)
                collection_incumbent_temp.delete_many(filter = incumbents_filter)


        return True

    except Exception as e:
        logger.error('Error with db_data_ship: {}'.format(str(e).strip()))
        raise




    