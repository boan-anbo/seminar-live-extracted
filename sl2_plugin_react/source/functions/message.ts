import {browser} from 'webextension-polyfill-ts';
import {Instruction, MESSAGE_OPERATION} from '../interfaces/Instruction';

export const instruct = async (instruction: Instruction) => {
  return browser.runtime.sendMessage(instruction);
};



export const testBackground = async () => {
  return instruct({
    operation: MESSAGE_OPERATION.TEST,
  } as Instruction);

};
