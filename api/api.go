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
	"net/http"
	"net/url"

	"github.com/gin-gonic/gin"
	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
	"github.com/retr0h/janus/pools"
	"github.com/spf13/viper"
)

func newPool() *pools.Pools {
	etcdServers := viper.GetStringSlice("backend.etcd.servers")
	etcdClient, _ := client.NewEtcdClient(etcdServers)
	labels, _ := labels.NewLabels(etcdClient)
	pools, _ := pools.NewPools(etcdClient, labels)

	return pools
}

// GetMainEngine return .....
func GetMainEngine() *gin.Engine {
	r := gin.Default()
	r.UseRawPath = viper.GetBool("server.use_raw_path")
	r.UnescapePathValues = viper.GetBool("server.unescape_path_values")
	pools := newPool()

	v1 := r.Group("/v1")
	{
		v1.GET("/pool/:id", func(c *gin.Context) {
			id := c.Param("id")
			decodedID, err := url.PathUnescape(id)
			if err != nil {
				// c.AbortWithError(http.StatusUnauthorized, errors.StatusInternalServerError).SetType(gin.ErrorTypePublic)
			}

			key, err := pools.GetPool("namespace", decodedID)

			if err != nil {
				// c.AbortWithError(http.StatusUnauthorized, errors.StatusInternalServerError).SetType(gin.ErrorTypePublic)
			}

			if key.Value == "" {
				c.String(http.StatusNotFound, "resource not found")
				return
			}

			c.JSON(http.StatusOK, gin.H{
				"namespace": "namespace",
				"id":        key.Value,
			})

		})

	}

	return r
}
