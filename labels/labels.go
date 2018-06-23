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

// Package labels provides primitives for managing labels.
package labels

import (
	"fmt"
	"sort"

	"github.com/retr0h/janus/client"
)

// Labels is an object which implements the `Labels` business logic interface.
type Labels struct {
	etcdClient client.EtcdClient
}

// NewLabels constructs a new `Labels`.
func NewLabels(e *client.EtcdClient) (*Labels, error) {
	return &Labels{
		etcdClient: *e,
	}, nil
}

// CreateLabel creates a Label.
func (l *Labels) CreateLabel(namespace string, label string, key string) error {
	labelKey := setLabelKey(namespace, label, key)
	if _, err := l.etcdClient.Put(labelKey, "foo"); err != nil {
		return err
	}

	return nil
}

// DeleteLabel deletes a Label.
func (l *Labels) DeleteLabel(namespace string, label string, key string) error {
	labelKey := setLabelKey(namespace, label, key)
	if _, err := l.etcdClient.Delete(labelKey); err != nil {
		return err
	}

	return nil
}

// GetLabel returns the requested Label.
func (l *Labels) GetLabel(namespace string, label string, key string) (client.EtcdItem, error) {
	labelKey := setLabelKey(namespace, label, key)
	k, err := l.etcdClient.Get(labelKey)

	if err != nil {
		return client.EtcdItem{}, err
	}

	if len(k) == 0 {
		return client.EtcdItem{}, nil
	}

	return k[0], nil
}

// GetLabels returns a list of Labels.
func (l *Labels) GetLabels(namespace string, label string) (client.EtcdCollection, error) {
	keyPrefix := getLabelPrefix(namespace, label)
	keys, err := l.etcdClient.GetWithPrefix(keyPrefix)
	if err != nil {
		return client.EtcdCollection{client.EtcdItem{}}, err
	}

	return keys, nil
}

func getAllLabels(namespace string, labels []string) []string {
	sortedLabels := make([]string, len(labels))
	copy(sortedLabels, labels)
	sort.Sort(sort.StringSlice(sortedLabels))

	prevItem := ""
	for _, item := range sortedLabels {
		if prevItem == "" {
			prevItem = item
			continue
		}

		prevItem = fmt.Sprintf("%s,%s", prevItem, item)
		sortedLabels = append(sortedLabels, prevItem)
	}

	return sortedLabels
}

func getLabelPrefix(namespace string, label string) string {
	return fmt.Sprintf("labels/%s/%s", namespace, label)
}

func setLabelKey(namespace string, label string, key string) string {
	return fmt.Sprintf("labels/%s/%s/%s", namespace, label, key)
}
