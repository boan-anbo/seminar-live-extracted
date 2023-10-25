import {MESSAGE_OPERATION} from '../interfaces/Instruction';
import {instruct} from './message';

export const searchBrowserEngine = async (query: string) => {
  const local = await instruct({
    operation: MESSAGE_OPERATION.SEARCH,
    payload: query
  });
  console.log("local received", local)

  return local
}

