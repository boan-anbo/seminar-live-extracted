import {Filter} from "../models/filter";
import {instruct} from "./message";
import {Instruction, MESSAGE_OPERATION} from "../interfaces/Instruction";

export const readFromClipboard = async (): Promise<string> => {
    return instruct({
        operation: MESSAGE_OPERATION.READ_FROM_CLIPBOARD,
    } as Instruction);
};
