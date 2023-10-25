import {Component} from "react";
import {IItem} from "./Item";

export class ItemList extends Component< {postWebinar: any, items: IItem[]}, {items: IItem[]}> {
    render() {
        return (


                <div className=''>

                    {this.props.items.map((item, index) => {
                        return (

                        <div>
                            <div>
                                <span>Title: {item.url}</span>
                                <button onClick={() => this.props.postWebinar(item)}>Post</button>
                            </div>
                                <div key={index}>{
                            Object.entries(item).map(([key, value]) => {
                                return (<div className="grid grid-cols-12 w-full text-center space-y-4 border-2">

                                        <div className="col-span-3 font-bold">{key}:</div> <div className="col-span-9 text-left px-8">{value}</div>
                                    </div>
                                )
                            })
                        }</div>


                        </div>

                        )
                    })}
                </div>

        );
    }
}
