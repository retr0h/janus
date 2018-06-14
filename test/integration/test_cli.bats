#!/usr/bin/env bats

@test "invoke janus without arguments prints usage" {
	run go run main.go

	[ "$status" -eq 0 ]
	echo "${output}" | grep "A restful port reservation microservice."
}

@test "invoke janus version subcommand" {
	run go run main.go version

	[ "$status" -eq 0 ]
	echo "${output}" | grep "Date:"
	echo "${output}" | grep "Build:"
	echo "${output}" | grep "Version:"
	echo "${output}" | grep "Git Hash:"
}
