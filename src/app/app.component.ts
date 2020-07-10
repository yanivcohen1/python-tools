import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'app';

  serverData: JSON;
  employeeData: JSON;
  employee: JSON;
  name: string;
  name2: string;

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
  }

  sayHi() {
    this.httpClient.get('http://127.0.0.1:5000/').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    });
  }

  getAllEmployees() {
    this.httpClient.get('http://127.0.0.1:5000/employees').subscribe((data: any) => {
      const names = data.employees.map(x => x.name);
      // this.names = data.employees[0].name
      this.employeeData = data as JSON;
      console.log(this.employeeData);
    });
  }
  getEmployee() {
    this.httpClient.get('http://127.0.0.1:5000/employees/1').subscribe((data: any) => {
      this.name = data.data.name;
      this.employee = data as JSON;
      console.log(this.employee);
    });
  }
}
