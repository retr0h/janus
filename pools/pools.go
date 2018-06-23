// Copyright (c) 2018 John Dewey

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to
// deal in the Software without restriction, including without limitation the
// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
// sell copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

// Package pools provides primitives for managing pools.
package pools

import (
	"fmt"

	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
)

// Pools interface defines the methods for implementing Pool related business
// logic.
// type Pools interface {
//     GetPools(string) ([]client.EtcdItem, error)
// }

// Pools is an object which implements the `Pools` business logic interface.
type Pools struct {
	etcdClient client.EtcdClient
	labels     labels.Labels
}

// NewPools constructs a new `Pools`.
func NewPools(e *client.EtcdClient, l *labels.Labels) (*Pools, error) {
	return &Pools{
		etcdClient: *e,
		labels:     *l,
	}, nil
}

// UpdatePool updates a Pool.
// DeletePool removes a Pool.

// CreatePool creates a Pool.
func (p *Pools) CreatePool(namespace string, cidr string) error {
	// TODO(retr0h): Needs to be in a transaction.
	key := poolsCidrKey(namespace, cidr)
	if _, err := p.etcdClient.Put(key, "foo"); err != nil {
		return err
	}

	// TODO(retr0h): Needs to be in a transaction.
	if err := p.labels.CreateLabel(namespace, "pools", cidr); err != nil {
		return err
	}

	return nil
}

// DeletePool deletes a Pool.
func (p *Pools) DeletePool(namespace string, cidr string) error {
	// TODO(retr0h): Needs to be in a transaction.
	key := poolsCidrKey(namespace, cidr)
	if _, err := p.etcdClient.Delete(key); err != nil {
		return err
	}

	// TODO(retr0h): Needs to be in a transaction.
	if err := p.labels.DeleteLabel(namespace, "pools", cidr); err != nil {
		return err
	}

	return nil
}

// GetPool returns the requested Pool.
func (p *Pools) GetPool(namespace string, cidr string) (client.EtcdItem, error) {
	keyPrefix := poolsCidrKey(namespace, cidr)
	key, err := p.etcdClient.Get(keyPrefix)
	if err != nil {
		return client.EtcdItem{}, err
	}

	if len(key) == 0 {
		return client.EtcdItem{}, nil
	}

	return key[0], nil
}

// GetPools returns a list of Pools.
func (p *Pools) GetPools(namespace string) (client.EtcdCollection, error) {
	keys, err := p.labels.GetLabels(namespace, "pools")
	if err != nil {
		return client.EtcdCollection{client.EtcdItem{}}, err
	}

	return keys, nil
}

func poolsCidrKey(namespace string, cidr string) string {
	return fmt.Sprintf("pools/%s/%s", namespace, cidr)
}
