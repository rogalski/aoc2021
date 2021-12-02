package main

import (
	"strconv"
	"testing"
)

func TestFinalPositionAndDepth(t *testing.T) {
	position, depth, err := finalPositionAndDepth("ex.txt")
	if err != nil {
		t.Errorf(err.Error())
	}
	if position != 15 {
		t.Errorf(strconv.Itoa(position))
	}
	if depth != 10 {
		t.Errorf(strconv.Itoa(depth))
	}
}

func TestFinalPositionAndDepthWithiAim(t *testing.T) {
	position, depth, err := finalPositionAndDepthWithAim("ex.txt")
	if err != nil {
		t.Errorf(err.Error())
	}
	if position != 15 {
		t.Errorf(strconv.Itoa(position))
	}
	if depth != 60 {
		t.Errorf(strconv.Itoa(depth))
	}
}
