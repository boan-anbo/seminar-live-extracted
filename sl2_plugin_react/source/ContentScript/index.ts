import {browser} from 'webextension-polyfill-ts';
import {testBackground} from '../functions/message';
import {Instruction, MESSAGE_OPERATION} from '../interfaces/Instruction';
import {getTabId} from "../functions/tabs";


let tabId = null

// @ts-ignore
const contentReducer = async (message, sender): Promise<string | undefined | null> => {


  console.log('Content Receive:', {message, sender});
  switch ((message as Instruction).operation) {
    case MESSAGE_OPERATION.GET_DOM_HTML:
      console.log('Content received request', sender);
      return document.documentElement.outerHTML;
    case MESSAGE_OPERATION.GET_TABID_FROM_CONTENT:
      return tabId
  }

  // console.log("Background prvodeds current tab id", tabId)
};

console.log('helloworld from content script');

browser.runtime.onMessage.addListener(contentReducer);

const onInit = async () => {
  tabId = await getTabId()
  console.log('Entire Dom', {domHtml: document.documentElement.outerHTML});
  const result = await testBackground();
  console.log('Content Received', {result});
};

setTimeout(() => onInit(), 2000);

export {};
