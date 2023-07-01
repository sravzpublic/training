#!/bin/sh
mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);
    db.grantRolesToUser({ role: "clusterAdmin", db: "admin" })
    use sravz;
    db.dropUser('sravz')
    db.createUser({user: 'sravz', pwd: 'sravz', roles: [
        {
        role: 'dbAdmin',
        db: 'sravz',
        },
        {
        role: 'readWrite',
        db: 'sravz',
        }
    ]});
EOF