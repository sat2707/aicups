//
// Copyright (c) 2016 iAchieved.it LLC
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
import Foundation

public protocol SocketDelegate {
  
}

public class Socket:NSObject, StreamDelegate {
  let host: String
  let port: Int
  fileprivate let readConditions = NSCondition()
  fileprivate let writeConditions = NSCondition()
  fileprivate let inputStream: InputStream
  fileprivate let outputStream: OutputStream
  fileprivate let readBuffer = UnsafeMutablePointer<uint8>.allocate(capacity: 1024)
  fileprivate var readData = Data()
  init(host:String, port:Int) {
    self.host = host
    self.port = port
    var input:InputStream?
    var out:OutputStream?
    Stream.getStreamsToHost(withName: host, port: port, inputStream: &input, outputStream: &out)
    inputStream = input!
    outputStream = out!
    super.init()
    inputStream.delegate = self;
    outputStream.delegate = self;
  }
  
  func connect() throws {
    Thread.detachNewThread {
      let runLoop = RunLoop.current
      self.inputStream.schedule(in: runLoop, forMode: .commonModes)
      self.outputStream.schedule(in: runLoop, forMode: .commonModes);
      self.inputStream.open()
      self.outputStream.open()
      while self.inputStream.streamStatus != .closed
      {
        runLoop.run(until: Date().addingTimeInterval(1))
      }
    }
  }
  
  func readLine() -> Data? {
    var line:Data!
    var appendingStart = 0
    while line == nil {
      if let eol = readData.subdata(in: appendingStart..<readData.endIndex).range(of: "\n".data(using: .utf8)!)
      {
        let lineRange:Range<Data.Index> = 0..<appendingStart+eol.upperBound
        line = readData.subdata(in: lineRange)
        readData.removeSubrange(lineRange)
      }
      if line == nil
      {
        self.readConditions.lock()
        if !inputStream.hasBytesAvailable
        {
          self.readConditions.wait()
        }
        self.readConditions.unlock()
        let read = inputStream.read(readBuffer, maxLength: 1024)
        if read == -1
        {
          return nil;
        }
        
        readData.append(readBuffer, count: read)
        appendingStart = readData.index(readData.count, offsetBy: -read)
      }
    }
    return line
  }
  
  func write(data: Data) {
    if !self.outputStream.hasSpaceAvailable
    {
      self.writeConditions.lock()
      self.writeConditions.wait()
      self.writeConditions.unlock()
    }
    
    let _ = data.withUnsafeBytes {
      outputStream.write($0, maxLength: data.count)
    }
  }
  
  deinit {
    readBuffer.deallocate(capacity: 1024)
  }
  
  public func stream(_ aStream: Stream, handle eventCode: Stream.Event) {
    
    switch (aStream,eventCode)
    {
    case(inputStream,.hasBytesAvailable):
      self.readConditions.lock()
      self.readConditions.signal()
      self.readConditions.unlock()
    case(outputStream,.openCompleted),(outputStream,.hasSpaceAvailable):
      self.writeConditions.lock()
      self.writeConditions.signal()
      self.writeConditions.unlock()
    case(_,.endEncountered),(_,.errorOccurred):
      self.inputStream.close()
      self.outputStream.close()
      self.readConditions.lock()
      self.readConditions.signal()
      self.readConditions.unlock()
      self.writeConditions.lock()
      self.writeConditions.signal()
      self.writeConditions.unlock()
    case (_, _): break
    }
    
  }
}

