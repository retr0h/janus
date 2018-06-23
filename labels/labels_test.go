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

package labels

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetAllLabels(t *testing.T) {
	labels := []string{"foo", "foo1", "foo2", "foo-bar", "foo-bar1", "qux"}
	result := getAllLabels("namespace", labels)

	x := []string{
		"foo",
		"foo-bar",
		"foo-bar1",
		"foo1",
		"foo2",
		"qux",
		"foo,foo-bar",
		"foo,foo-bar,foo-bar1",
		"foo,foo-bar,foo-bar1,foo1",
		"foo,foo-bar,foo-bar1,foo1,foo2",
		"foo,foo-bar,foo-bar1,foo1,foo2,qux",
	}

	assert.Equal(t, x, result)
}

func TestGetAllLabelsForSingleLabel(t *testing.T) {
	labels := []string{"foo"}
	result := getAllLabels("namespace", labels)

	assert.Equal(t, []string{"foo"}, result)
}

func TestGetLabelPrefix(t *testing.T) {
	result := getLabelPrefix("namespace", "pools")

	assert.Equal(t, "labels/namespace/pools", result)
}

func TestSetLabelKey(t *testing.T) {
	result := setLabelKey("namespace", "pools", "10.10.10.0/24")

	assert.Equal(t, "labels/namespace/pools/10.10.10.0/24", result)
}
