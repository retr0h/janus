# Schema

## Pools

Pools are created in the following keyspace.

    pools/:namespace/:cidr

Addresses belonging to a particular namespace's pool.

    pools/:namespace/:cidr/:address

Pools are created with a label.

    labels/:namespace/pools/:cidr

This allows Janus to find all pools allocated to a given namespace
by searching for the following key prefix with a simple query.

    labels/:namespace/pools/

## Labels

Labels are created under:

    labels/:namespace/:label/:key

Address objects can be assigned labels.  The address object can have
a maximum of `JANUS_MAX_LABEL_SIZE` (5) labels.

Janus will lexicographically sort the provided labels and create
reverse-indexes.  This allows Janus to return the address(es) based
on a selector in O(1).

Providing the following labels:

    - foo
    - bar
    - baz
    - qux

The following reverse-indexes are created.  This isn't very efficient,
due to number of keys stored in the backend.  However, lookups
are trivial.  For every label added Janus stores lookup keys
`len(total_labels) + (len(total_labels) -1)`.

    labels/:namespace/bar/:cidr
    labels/:namespace/baz/:cidr
    labels/:namespace/foo/:cidr
    labels/:namespace/qux/:cidr
    labels/:namespace/bar,baz/:cidr
    labels/:namespace/bar,baz,foo/:cidr
    labels/:namespace/bar,baz,foo,qux/:cidr

Labels are queried by lexicographically sorting them and joining with
a comma.  This provides a consistent way to lookup a label or combination
of labels.
