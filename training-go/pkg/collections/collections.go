// ref https://go101.org/article/container.html
// ref https://go.dev/doc/faq
package collections

import "log"

type linkedlist struct {
	node *node
}

type node struct {
	index int
	next  *node
	prev  *node
}

func Collection() {
	a := [4]bool{2: true, 1: true}
	// b := [4]bool{6: true, 1: true}
	log.Println(a)

	// Create a linked list of size 3
	ll := linkedlist{node: &node{index: 0}}
	current_node := ll.node
	for i := 1; i <= 9; i++ {
		current_node.next = &node{index: i}
		current_node.next.prev = current_node
		current_node = current_node.next
	}
	// Traverse the linked list and print the index
	current_node = ll.node
	for i := 0; i < 10; i++ {
		log.Println("Linked list node index: ", current_node.index)
		current_node = current_node.next
	}

}
