import { Component, OnInit } from '@angular/core';
import { OdgovorUcenika } from '../../models';
import { TestService } from '../../services/test.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-end-test',
  templateUrl: './end-test.component.html',
  styleUrls: ['./end-test.component.scss']
})
export class EndTestComponent implements OnInit {

  odgovori: OdgovorUcenika[];

  constructor(
      private testService: TestService,
      private router: Router,
      private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {
    this.getOdgovori();
  }

  getOdgovori() {
    const testUcenika = JSON.parse(sessionStorage.getItem('testUcenika'));
    this.testService.getRezime(testUcenika).subscribe(data => {
      console.log(data);
      this.odgovori = data;
    }, error => {
      const snackBarRef = this.snackBar.open(`Greška ${error.status}!`, 'OK');
      console.log(error);
    });
  }

  zavrsi(): void {
    const testUcenika = JSON.parse(sessionStorage.getItem('testUcenika'));
    this.testService.zavrsiTest(testUcenika).subscribe(data => {
      const snackBarRef = this.snackBar.open(`Test je završen!`, 'OK');
      snackBarRef.afterDismissed().subscribe(() => {
        this.router.navigate(['/']);
      });
    }, error => {
      const snackBarRef = this.snackBar.open(`Greška ${error.status}!`, 'OK');
      console.log(error);
    });
  }
}
