import argparse
import pymongo
import sys
import urllib

parser = argparse.ArgumentParser(description="Test K8S MongoDB application.")
parser.add_argument("--firstTime",
                    dest="FirstTime",
                    help="True if first time testing the application, False otherwise",
                    default=False,
                    action='store_true')
parser.add_argument("--url",
                    dest="URL",
                    help="URL of the database",
                    required=True)

testList = [
    {"brand": "Ford", "model": "Focus"},
    {"brand": "Volkswagen", "model": "Golf"},
    {"brand": "Renault", "model": "Megane"}
]


def getHostnamePort(url):
    urlParsed = urllib.parse.urlparse(url, allow_fragments=True)

    return urlParsed.hostname, urlParsed.port


def getMongoClient(hostname, port):
    return pymongo.MongoClient(
        host=hostname,
        port=port)


def main():
    args = parser.parse_args()

    firstTime = args.FirstTime
    url = args.URL

    hostname, port = getHostnamePort(url)

    mongoClient = getMongoClient(hostname, port)

    if firstTime:
        # Create database
        testDatabase = mongoClient['testDatabase']

        # Create collection
        testCollection = testDatabase['testCollection']

        # Insert documents
        result = testCollection.insert_many(testList)

        # Check that everything was created correctly
        databaseList = mongoClient.list_database_names()
        if "testDatabase" not in databaseList:
            sys.exit("Database was not created.")
        else:
            print("Database created.")

        collectionList = testDatabase.list_collection_names()
        if "testCollection" not in collectionList:
            sys.exit("Collection was not created.")
        else:
            print("Collection created.")

        assert len(result.inserted_ids) == 3
        print("Documents inserted.")
    else:
        sys.exit

        databaseList = mongoClient.list_database_names()
        if "testDatabase" not in databaseList:
            sys.exit("Database does not exist.")
        else:
            print("Database exists.")
            testDatabase = mongoClient['testDatabase']

        collectionList = testDatabase.list_collection_names()
        if "testCollection" not in collectionList:
            sys.exit("Collection does not exist.")
        else:
            print("Collection exists.")
            testCollection = testDatabase['testCollection']

        numberDocuments = testCollection.count_documents({})
        if numberDocuments != len(testList):
            print("Number of documents: %d".format(numberDocuments))
            sys.exit("The number of documents does not match:")
        else:
            print("Number of documents matches.")

        for document in testList:
            databaseDocument = testCollection.find({}, document)
            if not databaseDocument:
                sys.exit("Document not found.")
        print("All documents exist.")

if __name__ == "__main__":
    main()
