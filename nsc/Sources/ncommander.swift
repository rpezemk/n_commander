import Foundation
import Figlet
import ArgumentParser
import Cncurses

@main
struct FigletTool: ParsableCommand {
    @Option(help:"Specify the input")
    public var input: String

    public func run() throws {
        Figlet.say(self.input)




    }
}
// main to jest entrypoint w pliku mozna miec tylko jeden taki
// robimy to zamiast definiowac plik main.swift