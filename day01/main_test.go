package main

import "testing"

func TestDepthIncreaseCount(t *testing.T) {
	expected := 7
	got, err := depthIncreaseCount("ex01.txt")
	if err != nil {
		t.Errorf("Error: %s", err)
	}
	if expected != got {
		t.Errorf("Expected %d; was %d", expected, got)
	}
}

func TestDepthIncreaseCountWithSlidingWindow(t *testing.T) {
	expected := 5
	got, err := depthIncreaseCountWithSlidingWindow("ex01.txt", 3)
	if err != nil {
		t.Errorf("Error: %s", err)
	}
	if expected != got {
		t.Errorf("Expected %d; was %d", expected, got)
	}
}
