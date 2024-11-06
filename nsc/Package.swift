// swift-tools-version: 5.10
// The swift-tools-version declares the minimum version of Swift required to build this package.
// Package.swift
import PackageDescription

let package = Package(
    name: "SwiftNCursesApp",
    platforms: [
        .macOS(.v10_14)
    ],
    products: [
        .executable(name:"SwiftCom",targets:["SwiftCom"])
    ],
    dependencies:[
        // .package(),
        // .package(),
    ],
    targets:[
        .target(name:"SwiftCom",dependencies:[])
    ]
    
    
)
