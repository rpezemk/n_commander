// swift-tools-version: 5.10
// The swift-tools-version declares the minimum version of Swift required to build this package.
// Package.swift
import PackageDescription

let package = Package(
    name: "NCommander",
    platforms: [
        .macOS(.v10_14)
    ],
    products: [
        .executable(name:"nsc",targets:["nsc"])
    ],
    dependencies:[
        .package(url: "https://github.com/apple/example-package-figlet", branch: "main"),
        .package(url: "https://github.com/apple/swift-argument-parser", from: "1.0.0"),
        // .package(),
        // .package(),
    ],
    targets:[
        .executableTarget(
            name:"nsc",
            dependencies:[
                .product(name:"Figlet",package:"example-package-figlet"),
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ],
            path:"Sources"),
    ]
    
    
)
