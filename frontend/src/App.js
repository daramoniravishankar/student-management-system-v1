import React, { useEffect, useState } from "react";
import "./App.css";

function App() {

const [students,setStudents] = useState([]);
const [name,setName] = useState("");
const [course,setCourse] = useState("");
const [grade,setGrade] = useState("");
const [editId,setEditId] = useState(null);

useEffect(()=>{

fetch("http://localhost:5000/students")
.then(res=>res.json())
.then(data=>setStudents(data))

},[])


const addStudent = () => {

if(!name || !course || !grade){
alert("Please fill all fields")
return
}

fetch("http://localhost:5000/students",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({name,course,grade})
}).then(()=>window.location.reload())

}


const deleteStudent = (id) => {

fetch(`http://localhost:5000/students/${id}`,{
method:"DELETE"
}).then(()=>window.location.reload())

}


const editStudent = (student) => {

setEditId(student.id)
setName(student.name)
setCourse(student.course)
setGrade(student.grade)

}


const updateStudent = () => {

fetch(`http://localhost:5000/students/${editId}`,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({name,course,grade})
}).then(()=>window.location.reload())

}


return(

<div className="app">

<div className="header">

<img
src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png"
alt="students"
/>

<h1>Student Management System</h1>

<p>Manage student records easily</p>

</div>


<div className="formCard">

<input
placeholder="Student Name"
value={name}
onChange={(e)=>setName(e.target.value)}
/>

<input
placeholder="Course"
value={course}
onChange={(e)=>setCourse(e.target.value)}
/>

<input
placeholder="Grade"
value={grade}
onChange={(e)=>setGrade(e.target.value)}
/>


{editId ? (
<button className="updateBtn" onClick={updateStudent}>
Update Student
</button>
) : (
<button className="addBtn" onClick={addStudent}>
Add Student
</button>
)}

</div>



<div className="tableContainer">

<table>

<thead>
<tr>
<th>ID</th>
<th>Name</th>
<th>Course</th>
<th>Grade</th>
<th>Actions</th>
</tr>
</thead>

<tbody>

{students.map((s)=>(
<tr key={s.id}>

<td>{s.id}</td>
<td>{s.name}</td>
<td>{s.course}</td>
<td>{s.grade}</td>

<td>

<button
className="editBtn"
onClick={()=>editStudent(s)}
>
Edit
</button>

<button
className="deleteBtn"
onClick={()=>deleteStudent(s.id)}
>
Delete
</button>

</td>

</tr>
))}

</tbody>

</table>

</div>

</div>

)

}

export default App