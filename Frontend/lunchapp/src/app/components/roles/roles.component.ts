import { AfterViewInit, Component, ViewChild, Input, OnInit } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { Observable } from 'rxjs';
import { ShowRole } from '../../models/index';
import { getRoles } from 'src/app/selectors/index.selectors';
import {Store,select}  from '@ngrx/store';
import { AppState } from 'src/app/reducers';

@Component({
  selector: 'app-roles',
  templateUrl: './roles.component.html',
  styleUrls: ['./roles.component.scss']
})
export class RolesComponent implements  OnInit {
  listData: MatTableDataSource<any> = new MatTableDataSource()
  public roleList: Observable<ShowRole[]>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['id', 'name','description', 'dateAdded', 'actions' ];
  searchKey: string ='';
  constructor(private store: Store<AppState>,) {
    this.roleList = this.store.pipe(select(getRoles));

  }
  ngOnInit(): void {
    this.roleList.subscribe((data) => {
      if (data){
      console.log(data)
      this.listData = new MatTableDataSource(data);
    }
  });
  this.listData.sort = this.sort;
  this.listData.paginator = this.paginator;
  // this.listData.filterPredicate = (data, filter) => {
  //   return this.displayedColumns.some(ele => {
  //     return ele != 'actions' && data[ele].toLowerCase().indexOf(filter) != -1;
  //   });
  // }
  }


  onSearchClear() {
    this.searchKey = "";
    this.applyFilter();
  }

  applyFilter() {
    this.listData.filter = this.searchKey.trim().toLowerCase();
  }

  onCreate() {}
  onEdit(row:any){}
  onDelete($id:number){}
}
