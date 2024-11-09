import { JSDOM } from 'jsdom';

const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`)

console.log(dom.window.document.querySelector('p')?.textContent)
// "Hello world"

// const { window } = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`)
// const { document } = window
// document.querySelector('p').textContent // "Hello world"
