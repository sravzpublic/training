package asset

import "log"

// Interface composition
type asset interface {
	int | float64
}

func Print[T asset](t T) {
	log.Println("This is T: ", t)
}
