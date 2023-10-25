import {MESSAGE_OPERATION} from "../interfaces/Instruction";
import {instruct} from "./message";

export const getTabId = async () => {
  return instruct({
    operation: MESSAGE_OPERATION.GET_CURRENT_TAB_ID,
  });
};

export const getTabUrl = async () => {
  const local = await instruct({
    operation: MESSAGE_OPERATION.GET_CURRENT_TAB_URL,
  });
  console.log("local received", local)

  return local
}

