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

package pools_test

import (
	"testing"

	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
	"github.com/retr0h/janus/pools"
	testutils "github.com/retr0h/janus/test/utils"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
)

type PoolsTestSuite struct {
	suite.Suite
	pools      pools.Pools
	labels     labels.Labels
	etcdClient client.EtcdClient
}

func init() {
	testutils.ViperInit()
}

func (suite *PoolsTestSuite) SetupTest() {
	etcdServers := viper.GetStringSlice("backend.etcd.servers")
	etcdClient, _ := client.NewEtcdClient(etcdServers)
	labels, _ := labels.NewLabels(etcdClient)
	pools, _ := pools.NewPools(etcdClient, labels)

	suite.pools = *pools
	suite.labels = *labels
	suite.etcdClient = *etcdClient
}

func (suite *PoolsTestSuite) TearDownTest() {
	// ignore
}

func (suite *PoolsTestSuite) TestCreatePool() {
	err := suite.pools.CreatePool("namespace", "10.10.10.0/24")
	assert.NoError(suite.T(), err)

	key, _ := suite.pools.GetPool("namespace", "10.10.10.0/24")
	assert.Equal(suite.T(), "pools/namespace/10.10.10.0/24", key.Key)

	suite.pools.DeletePool("namespace", "10.10.10.0/24")
}

func (suite *PoolsTestSuite) TestDeletePool() {
	suite.pools.CreatePool("namespace", "10.10.10.0/24")

	err := suite.pools.DeletePool("namespace", "10.10.10.0/24")
	assert.NoError(suite.T(), err)

	key, _ := suite.pools.GetPool("namespace", "10.10.10.0/24")
	assert.Equal(suite.T(), client.EtcdItem{}, key)

	key, _ = suite.labels.GetLabel("namespace", "pools", "10.10.10.0/24")
	assert.Equal(suite.T(), client.EtcdItem{}, key)
}

func (suite *PoolsTestSuite) TestGetPool() {
	suite.etcdClient.Put("pools/namespace/10.10.10.0/24", "foo")

	key, err := suite.pools.GetPool("namespace", "10.10.10.0/24")
	assert.Equal(suite.T(), "pools/namespace/10.10.10.0/24", key.Key)
	assert.NoError(suite.T(), err)

	suite.pools.DeletePool("namespace", "10.10.10.0/24")
}

func (suite *PoolsTestSuite) TestGetPoolReturnsEmptyEtcdClientOnMissingPool() {
	key, err := suite.pools.GetPool("namespace", "invalid")
	assert.Equal(suite.T(), client.EtcdItem{}, key)
	assert.NoError(suite.T(), err)
}

func (suite *PoolsTestSuite) TestGetPools() {
	suite.pools.CreatePool("namespace", "10.10.10.0/24")
	suite.pools.CreatePool("namespace", "20.20.20.0/24")

	keys, err := suite.pools.GetPools("namespace")
	assert.Equal(suite.T(), 2, len(keys))
	assert.NoError(suite.T(), err)

	suite.pools.DeletePool("namespace", "10.10.10.0/24")
	suite.pools.DeletePool("namespace", "20.20.20.0/24")
}

func (suite *PoolsTestSuite) TestGetPoolsReturnsEmptyListOnMissingPools() {
	keys, err := suite.pools.GetPools("invalid")
	assert.Equal(suite.T(), 0, len(keys))
	assert.NoError(suite.T(), err)
}

// In order for `go test` to run this suite, we need to create
// a normal test function and pass our suite to suite.Run.
func TestPoolsTestSuite(t *testing.T) {
	suite.Run(t, new(PoolsTestSuite))
}
