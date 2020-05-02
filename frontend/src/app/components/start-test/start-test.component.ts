import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { TestService } from '../../services/test.service';
import { Test } from '../../models';
import { Observable } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-start-test',
  templateUrl: './start-test.component.html',
  styleUrls: ['./start-test.component.scss']
})
export class StartTestComponent implements OnInit {

  testID: number;
  test: Test;

  constructor(
      private activatedRoute: ActivatedRoute,
      private router: Router,
      private snackBar: MatSnackBar,
      private testService: TestService
  ) { }

  ngOnInit(): void {
    this.activatedRoute.paramMap.pipe(
      switchMap((params: ParamMap, index: number) => {
        this.testID = +params.get('id');
        return this.testService.getTest(this.testID);
      })).subscribe(data => {
        this.test = data;
      }, console.log
    );
  }

  pocni(): void {
    this.testService.fetchTest(this.testID).subscribe(data => {
      this.testService.setTest(data);
      sessionStorage.setItem('pitanja', JSON.stringify(this.testService.test));
      this.testService.zapocniTest(this.testID).subscribe(test => {
        sessionStorage.setItem('testUcenika', JSON.stringify(test.test_ucenika));
        this.router.navigate(['/pitanje', 1]);
      }, error => {
        if (error.status === 409) {
          const snackBarRef = this.snackBar.open('Već ste počeli popunjavanje testa!', 'OK');
          snackBarRef.afterDismissed().subscribe(() => {
            this.router.navigate(['/pitanje', 1]);
          });
        } else {
          const snackBarRef = this.snackBar.open(`Greška ${error.status}!`, 'OK');
          console.log(error);
        }
      });
    }, console.log);
  }
}
