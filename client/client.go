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

// Package client provides primitives for accessing etcd.
package client

import (
	"context"
	"time"

	"github.com/coreos/etcd/clientv3"
)

// EtcdClient for accessing Etcd.
type EtcdClient struct {
	client         clientv3.Client
	requestTimeout time.Duration
}

// EtcdItem contains information about the key fetched.
type EtcdItem struct {
	Key   string // Key stored in etcd.
	Value string // Value assigned to `Key`.
}

// EtcdCollection contains a collection of `EtcdItems`.
type EtcdCollection []EtcdItem

// NewEtcdClient constructs a new `EtcdClient`.
func NewEtcdClient(etcdURI []string) (*EtcdClient, error) {
	cfg := clientv3.Config{
		Endpoints:   etcdURI,
		DialTimeout: 5 * time.Second,
	}

	etcdClient, err := clientv3.New(cfg)
	if err != nil {
		return nil, err
	}

	return &EtcdClient{
		client:         *etcdClient,
		requestTimeout: 5 * time.Second,
	}, nil
}

// Delete deletes a key in Etcd.
func (e *EtcdClient) Delete(key string, opts ...clientv3.OpOption) (*clientv3.DeleteResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), e.requestTimeout)
	defer cancel()

	return e.client.Delete(ctx, key, opts...)
}

// Get gets key(s) in Etcd.  Returns an empty slice if key is not found.
// When passed WithRange(), Get will return the key(s) matching the provide key prefix.
func (e *EtcdClient) Get(key string, opts ...clientv3.OpOption) (EtcdCollection, error) {
	ctx, cancel := context.WithTimeout(context.Background(), e.requestTimeout)
	defer cancel()
	response, err := e.client.Get(ctx, key, opts...)

	if err != nil {
		return EtcdCollection{EtcdItem{}}, err
	}

	etcdCollection := EtcdCollection{}
	for _, item := range response.Kvs {
		etcdItem := EtcdItem{
			Key:   string(item.Key),
			Value: string(item.Value),
		}
		etcdCollection = append(etcdCollection, etcdItem)
	}

	return etcdCollection, nil
}

// GetWithPrefix gets key(s) from Etcd matching the provided key prefix.
func (e *EtcdClient) GetWithPrefix(keyPrefix string) (EtcdCollection, error) {
	return e.Get(keyPrefix, clientv3.WithPrefix())
}

// Put sets a value in Etcd.
func (e *EtcdClient) Put(key, value string, opts ...clientv3.OpOption) (*clientv3.PutResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), e.requestTimeout)
	defer cancel()

	return e.client.Put(ctx, key, value, opts...)
}
