// ref: https://gobyexample.com/sorting-by-functions
package util

import (
	"context"
	"fmt"
)

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

type ContextKey string

func EmptyContextFunction(ctx context.Context, contextType string) {
	fmt.Printf("Doing something! Type - %s - Value - %s\n", contextType, ctx.Value(ContextKey("key1")))
}

func ParentContextFunction(ctx context.Context, contextType string) {
	fmt.Printf("Before calling child! Type - %s - Value - %s\n", contextType, ctx.Value(ContextKey("key1")))
	childCtx := context.WithValue(ctx, ContextKey("key1"), "childValue")
	ChildContextFunction(childCtx, "withValue")
	fmt.Printf("After calling child! Type - %s - Value - %s\n", contextType, ctx.Value(ContextKey("key1")))
}

func ChildContextFunction(ctx context.Context, contextType string) {
	fmt.Printf("Child context function Doing something! Type - %s - Value - %s\n", contextType, ctx.Value(ContextKey("key1")))
}

func CancellableContext(ctx context.Context, dataCh chan int) {
	go func() {
		println("Staring busy loop")
		for {
			select {
			case <-ctx.Done():
				fmt.Println("Cancellable Context done!!!")
				// The context is over, stop processing results
				return
			case i := <-dataCh:
				fmt.Println("Data: ", i)
				// Process the results received
			}
		}
	}()
}

func ContextWithDeadline(ctx context.Context, dataCh chan int) {
	go func() {
		println("Staring busy loop")
		for {
			select {
			case <-ctx.Done():
				fmt.Println("Deadline expired. Context with deadline done!!!")
				// The context is over, stop processing results
				return
			case i := <-dataCh:
				fmt.Println("Data: ", i)
				// Process the results received
			}
		}
	}()
}

func ContextWithTimeout(ctx context.Context, dataCh chan int) {
	go func() error {
		println("Staring busy loop")
		for {
			select {
			case <-ctx.Done():
				fmt.Println("Deadline expired. Context with timout done!!!")
				// The context is over, stop processing results
				return ctx.Err()
			case i := <-dataCh:
				fmt.Println("Data: ", i)
				// Process the results received
			}
		}
	}()
}
