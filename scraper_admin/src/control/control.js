import {Component} from "react";

export class Control extends Component {
    render() {
        return <>
            <div>Target Url: {this.props.targetUrl}</div>
            <input className="border-2" type="text" value={this.props.targetUrl} onChange={this.props.updateUrl}/>

            <button onClick={this.props.fetchItem}>Fetch Urls</button>
            <button onClick={this.props.pastFromClipboard}>Paste From Clipboard</button>
        </>;
    }
}
