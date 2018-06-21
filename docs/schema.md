# Schema

## Pools

Pools are created in the following keyspace.

    pools/:namespace/:cidr

Addresses belonging to a particular namespace's pool.

    pools/:namespace/:cidr/:address

## Labels

Pools are created with a label.

    pools/:namespace/labels/pool/:cidr

This allows Janus to find all pools allocated to a given namespace
by searching for the following key prefix with a simple query.

    pools/:namespace/labels/pool/
