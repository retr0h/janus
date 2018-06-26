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
	"net/url"

	"github.com/gin-gonic/gin"
	"github.com/retr0h/janus/client"
	"github.com/retr0h/janus/labels"
	"github.com/retr0h/janus/pools"
)

func newPool() *pools.Pools {
	etcdClient, _ := client.NewEtcdClient([]string{
		"http://etcd-0:2379",
		"http://etcd-1:2379",
		"http://etcd-2:2379",
	})
	labels, _ := labels.NewLabels(etcdClient)
	pools, _ := pools.NewPools(etcdClient, labels)

	return pools
}

// GetMainEngine return .....
func GetMainEngine() *gin.Engine {
	r := gin.Default()
	r.UseRawPath = true
	r.UnescapePathValues = false
	pools := newPool()

	v1 := r.Group("/v1")
	{
		v1.GET("/pool/:id", func(c *gin.Context) {
			id := c.Param("id")
			decodedID, err := url.PathUnescape(id)
			if err != nil {
				//
			}

			key, err := pools.GetPool("namespace", decodedID)

			if err != nil {
				//
			}

			c.JSON(200, gin.H{
				"namespace": "namespace",
				"id":        key.Value,
			})

		})

	}

	return r
}

func main() {
	GetMainEngine().Run(":8080")
}
