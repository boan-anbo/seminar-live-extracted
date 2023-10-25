import './App.css';
import {Component} from "react";
import {Control} from "./control/control";
import {v4} from 'uuid';
import axios from "axios";
import {ItemList} from "./ItemList";
import {IItem} from "./Item";

interface IState {items: IItem[], targetUrl: string}
class App extends Component<{}, IState> {
  state: IState
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      targetUrl: ''
    }
  }

  pasteFromClipbaord = async () => {
    const  targetUrl = await navigator.clipboard.readText()
    this.setState({targetUrl})
    // console.log(text)
  }

  fetchItem = async() => {
    const request = {
      jsonrpc: '2.0',
      id: v4(),
      method: "sc_health",
      params: {
        urls: [this.state.targetUrl]
      }
    }
    try {
      const {data} = await axios.post("http://localhost:8000/rpc_api/", request)
      const items = JSON.parse(data.result)
      console.log(items)
      this.setState({items})
    } catch(e) {
      console.error(e)
    }
  }

  postItem = async(item: IItem) => {
    console.log("Posting", item)
  }

  render() {
    // @ts-ignore
    return (
        <div className="">
          <Control
              fetchItem={this.fetchItem}
              targetUrl={this.state.targetUrl}
              updateUrl={(e) => this.setState({targetUrl: e.target.value})}
              pastFromClipboard={this.pasteFromClipbaord}/>

              <ItemList
                  items={this.state.items}
                  postWebinar={this.postItem}
              />

        </div>
    );
  }
}

export default App;
