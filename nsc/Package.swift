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
        .executable(name:"NCommander",targets:["ncommander"])
    ],
    dependencies:[
        .package(url: "https://github.com/apple/example-package-figlet", branch: "main")
        // .package(),
        // .package(),
    ],
    targets:[
        .executableTarget(
            name:"ncommander",
            dependencies:[
                .product(name:"Figlet",package:"example-package-figlet"),
            ],
            path:"Sources"),
    ]
    
    
)
