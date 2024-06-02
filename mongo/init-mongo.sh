#!/bin/sh
mongod &

mongo -- "$MONGO_INIT_DATABASE" <<EOF
var rootUser = '$MONGO_ADMIN_USERNAME';
var rootPassword = '$MONGO_ADMIN_PASSWORD';
var rootDb = '$MONGO_INIT_DATABASE';
var piUser = '$MONGO_PI_USERNAME';
var piPassword = '$MONGO_PI_PASSWORD';
var piDb = '$MONGO_PI_DATABASE';
db.getSiblingDB(rootUser).runCommand({authSchemaUpgrade: 1});
db.createUser(
  {
    user: rootUser,
    pwd: rootPassword,
    roles: [ "userAdminAnyDatabase","readWriteAnyDatabase" ]
  }
);
db.createUser(
  {
    user: piUser,
    pwd: piPassword,
    roles: [ { role: "readWrite", db: piDb } ]
  }
);
EOF
echo "Removing mongod.lock file"
rm -rf /data/db/mongod.lock
mongod --repair
mongod --shutdown
mongod --auth
