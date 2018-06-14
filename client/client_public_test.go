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

package client_test

import (
	"fmt"
	"testing"

	"github.com/retr0h/janus/client"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
)

type EtcdClientTestSuite struct {
	suite.Suite
	etcd client.EtcdClient
}

func (suite *EtcdClientTestSuite) SetupTest() {
	etcd, _ := client.NewEtcdClient([]string{
		"http://etcd-0:2379",
		"http://etcd-1:2379",
		"http://etcd-2:2379",
	})
	suite.etcd = *etcd
}

func (suite *EtcdClientTestSuite) TearDownTest() {
	// ignore
}

func (suite *EtcdClientTestSuite) TestDelete() {
	suite.etcd.Put("foo", "bar")

	suite.etcd.Delete("foo")

	key, err := suite.etcd.Get("foo")
	fmt.Println(key)

	assert.Equal(suite.T(), "", key)
	assert.NoError(suite.T(), err)
}

func (suite *EtcdClientTestSuite) TestDeleteDoesNotErrorOnMissingKey() {
	_, err := suite.etcd.Delete("invalid")

	// assert.Equal(suite.T(), "", key)
	assert.NoError(suite.T(), err)
}

func (suite *EtcdClientTestSuite) TestGet() {
	suite.etcd.Put("foo", "bar")

	key, err := suite.etcd.Get("foo")

	assert.Equal(suite.T(), "bar", key)
	assert.NoError(suite.T(), err)

	suite.etcd.Delete("foo")
}

func (suite *EtcdClientTestSuite) TestGetReturnsEmptyOnMissingKey() {
	key, err := suite.etcd.Get("invalid")

	assert.Equal(suite.T(), "", key)
	assert.NoError(suite.T(), err)
}

func (suite *EtcdClientTestSuite) TestPut() {
	suite.etcd.Put("foo", "bar")

	key, err := suite.etcd.Get("foo")

	assert.Equal(suite.T(), "bar", key)
	assert.NoError(suite.T(), err)

	suite.etcd.Delete("foo")
}

// In order for `go test` to run this suite, we need to create
// a normal test function and pass our suite to suite.Run.
func TestClientTestSuite(t *testing.T) {
	suite.Run(t, new(EtcdClientTestSuite))
}
