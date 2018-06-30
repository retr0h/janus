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

package labels_test

import (
	"testing"

	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
	testutils "github.com/retr0h/janus/test/utils"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
)

type LabelsTestSuite struct {
	suite.Suite
	labels     labels.Labels
	etcdClient client.EtcdClient
}

func init() {
	testutils.ViperInit()
}

func (suite *LabelsTestSuite) SetupTest() {
	etcdServers := viper.GetStringSlice("backend.etcd.servers")
	etcdClient, _ := client.NewEtcdClient(etcdServers)
	labels, _ := labels.NewLabels(etcdClient)

	suite.labels = *labels
	suite.etcdClient = *etcdClient
}

func (suite *LabelsTestSuite) TearDownTest() {
	// ignore
}

func (suite *LabelsTestSuite) TestCreateLabel() {
	err := suite.labels.CreateLabel("namespace", "pools", "10.10.10.0/24")
	assert.NoError(suite.T(), err)

	key, _ := suite.labels.GetLabel("namespace", "pools", "10.10.10.0/24")
	assert.Equal(suite.T(), "labels/namespace/pools/10.10.10.0/24", key.Key)

	suite.labels.DeleteLabel("namespace", "pools", "10.10.10.0/24")
}

func (suite *LabelsTestSuite) TestDeleteLabel() {
	suite.labels.CreateLabel("namespace", "pools", "10.10.10.0/24")

	err := suite.labels.DeleteLabel("namespace", "pools", "10.10.10.0/24")
	assert.NoError(suite.T(), err)

	key, _ := suite.labels.GetLabel("namespace", "pools", "10.10.10.0/24")
	assert.Equal(suite.T(), client.EtcdItem{}, key)
}

func (suite *LabelsTestSuite) TestGetLabel() {
	suite.labels.CreateLabel("namespace", "pools", "10.10.10.0/24")

	key, err := suite.labels.GetLabel("namespace", "pools", "10.10.10.0/24")
	assert.Equal(suite.T(), "labels/namespace/pools/10.10.10.0/24", key.Key)
	assert.NoError(suite.T(), err)

	suite.labels.DeleteLabel("namespace", "pools", "10.10.10.0/24")
}

func (suite *LabelsTestSuite) TestGetLabels() {
	suite.labels.CreateLabel("namespace", "pools", "10.10.10.0/24")
	suite.labels.CreateLabel("namespace", "pools", "20.20.20.0/24")

	keys, err := suite.labels.GetLabels("namespace", "pools")
	assert.Equal(suite.T(), 2, len(keys))
	assert.NoError(suite.T(), err)

	suite.labels.DeleteLabel("namespace", "pools", "10.10.10.0/24")
	suite.labels.DeleteLabel("namespace", "pools", "20.20.20.0/24")
}

// In order for `go test` to run this suite, we need to create
// a normal test function and pass our suite to suite.Run.
func TestLabelsTestSuite(t *testing.T) {
	suite.Run(t, new(LabelsTestSuite))
}
