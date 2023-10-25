import {browser} from 'webextension-polyfill-ts';
import {MESSAGE_OPERATION} from '../interfaces/Instruction';
import {getTabId} from './tabs';

export const getCurrentDomHtml = async () => {
  const activeTabId = await getTabId();
  return browser.tabs.sendMessage(activeTabId, {
    operation: MESSAGE_OPERATION.GET_DOM_HTML,
  });
};
