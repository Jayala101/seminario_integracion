import { UseStateInput } from '../src/UseStateInput.tsx'
import { UseStateSuma } from '../src/UseStateSuma.tsx'
import { UseRefAreaRectangulo } from '../src/UseRefAreaRectangulo.tsx'
import { UseRefAreaTrapecio } from '../src/UseRefAreaTrapecio.tsx'
import './App.css'

function App() {

  return (
    <>
      <UseStateInput/>
      <UseStateSuma/>
      <UseRefAreaRectangulo/>
      <UseRefAreaTrapecio/>
    </>
  )
}

export default App