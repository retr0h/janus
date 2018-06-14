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
	client         *clientv3.Client
	requestTimeout time.Duration
}

// NewEtcdClient constructs a new `EtcdClient`.
func NewEtcdClient(etcdURI []string) (*EtcdClient, error) {
	cfg := clientv3.Config{
		Endpoints:   etcdURI,
		DialTimeout: 5 * time.Second,
	}

	etcd, err := clientv3.New(cfg)
	if err != nil {
		return nil, err
	}
	return &EtcdClient{
		client:         etcd,
		requestTimeout: 5 * time.Second,
	}, nil
}

// Delete a key in Etcd.
func (etcdClient *EtcdClient) Delete(key string, opts ...clientv3.OpOption) (*clientv3.DeleteResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), etcdClient.requestTimeout)
	defer cancel()
	return etcdClient.client.Delete(ctx, key, opts...)
}

// Get gets a value in Etcd.  Returns an empty string if key is not found.
func (etcdClient *EtcdClient) Get(key string, opts ...clientv3.OpOption) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), etcdClient.requestTimeout)
	defer cancel()
	response, err := etcdClient.client.Get(ctx, key, opts...)

	if err != nil {
		return "", err
	}

	if response != nil && len(response.Kvs) == 0 {
		return "", err
	}

	return string(response.Kvs[0].Value), nil

}

// Put sets a value in Etcd.
func (etcdClient *EtcdClient) Put(key, value string, opts ...clientv3.OpOption) (*clientv3.PutResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), etcdClient.requestTimeout)
	defer cancel()
	return etcdClient.client.Put(ctx, key, value, opts...)
}

// func main() error {
//     return nil
// }
