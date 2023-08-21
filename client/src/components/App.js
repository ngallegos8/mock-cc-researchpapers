import { Route, Switch } from "react-router";
import Home from "./Home";


function App() {
  return (
    <>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </>
  );
}

export default App;
