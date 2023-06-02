// ref: https://gobyexample.com/sorting-by-functions
package util

type StringSlice []string

func (s StringSlice) Len() int {
	return len(s)
}
func (s StringSlice) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}
func (s StringSlice) Less(i, j int) bool {
	return len(s[i]) < len(s[j])
}
