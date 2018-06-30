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

package api

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
	"github.com/retr0h/janus/pools"
	testutils "github.com/retr0h/janus/test/utils"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/suite"
)

type APITestSuite struct {
	suite.Suite
	// TODO: Temporary
	pools pools.Pools
}

func init() {
	testutils.ViperInit()
}

func (suite *APITestSuite) SetupTest() {
	gin.SetMode(gin.TestMode)
	etcdServers := viper.GetStringSlice("backend.etcd.servers")
	etcdClient, _ := client.NewEtcdClient(etcdServers)
	labels, _ := labels.NewLabels(etcdClient)
	pools, _ := pools.NewPools(etcdClient, labels)

	suite.pools = *pools
}

func (suite *APITestSuite) TearDownTest() {
	// ignore
}

func (suite *APITestSuite) TestGetPool() {
	// TODO: Switch out
	suite.pools.CreatePool("namespace", "10.10.10.0/24")

	id := url.PathEscape("10.10.10.0/24")
	path := fmt.Sprintf("/v1/pool/%s", id)
	resp := performRequest("GET", path, GetMainEngine())

	assert.Equal(suite.T(), http.StatusOK, resp.Code)
	assert.Equal(suite.T(), `{"id":"foo","namespace":"namespace"}`, resp.Body.String())
	assert.Equal(suite.T(), "application/json; charset=utf-8", resp.Header().Get("Content-Type"))

	// TODO switch out
	suite.pools.DeletePool("namespace", "10.10.10.0/24")
}

func performRequest(method, target string, router *gin.Engine) *httptest.ResponseRecorder {
	r := httptest.NewRequest(method, target, nil)
	w := httptest.NewRecorder()
	router.ServeHTTP(w, r)

	return w
}

// In order for `go test` to run this suite, we need to create
// a normal test function and pass our suite to suite.Run.
func TestPoolsTestSuite(t *testing.T) {
	suite.Run(t, new(APITestSuite))
}
