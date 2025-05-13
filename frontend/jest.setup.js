// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom'

// Polyfills for web APIs
const { TextEncoder, TextDecoder } = require('util')
global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

// Mock web APIs
global.Request = class Request {
  constructor(url, options) {
    this.url = url
    this.options = options
  }
}

global.Response = class Response {
  constructor(body, options) {
    this.body = body
    this.options = options
  }
  json() {
    return Promise.resolve(this.body)
  }
}

// Mock next/headers
jest.mock('next/headers', () => ({
  cookies: jest.fn().mockReturnValue({
    get: jest.fn().mockReturnValue({ value: 'test-token' })
  })
})) 