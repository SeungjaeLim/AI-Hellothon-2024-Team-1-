from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app import schemas, crud, database, models

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
def get_weekly_tasks(
    year: int,
    week_number: int,
    db: Session = Depends(database.get_db),
):
    """
    Retrieve all tasks for the given year and week number.
    If a task does not exist for an elder, create it with status 0.
    Update the task status based on conditions:
      - If a record exists for the week, change status 0 -> 1
      - If a guide exists for the week, change status 1 -> 2
      - If the guide has been studied, change status 2 -> 3
    """
    # Calculate the start and end dates for the given week
    start_date = datetime.strptime(f"{year}-{week_number}-1", "%Y-%W-%w")
    end_date = start_date + timedelta(days=6)

    # Get all elders
    elders = crud.get_all_elders(db)
    if not elders:
        raise HTTPException(status_code=404, detail="No elders found")

    tasks = []

    for elder in elders:
        # Check if the task already exists
        task = crud.get_task_by_elder_year_week(db, elder_id=elder.id, year=year, week_number=week_number)

        # If not, create a new task with status 0
        if not task:
            task = models.Task(
                elder_id=elder.id,
                year=year,
                week_number=week_number,
                status=0,
            )
            db.add(task)
            db.commit()
            db.refresh(task)

        # Check for records created this week
        records_exist = (
            db.query(models.Record)
            .filter(
                models.Record.elder_id == elder.id,
                models.Record.created_at >= start_date,
                models.Record.created_at <= end_date,
            )
            .first()
        )
        if records_exist:
            task.status = max(task.status, 1)

        # Check for activity guides created this week
        guides_exist = (
            db.query(models.ActivityGuide)
            .filter(
                models.ActivityGuide.elder_id == elder.id,
                models.ActivityGuide.created_at >= start_date,
                models.ActivityGuide.created_at <= end_date,
            )
            .first()
        )
        if guides_exist:
            task.status = max(task.status, 2)

            # If the guide has been studied, update the status to 3
            if guides_exist.have_studied:
                task.status = max(task.status, 3)

        # Save changes to the database
        db.commit()
        db.refresh(task)

        tasks.append(task)

    return tasks

@router.get("/this_week", response_model=List[schemas.Task])
def get_tasks_for_this_week(
    db: Session = Depends(database.get_db),
):
    """
    Retrieve all tasks for the current week.
    If a task does not exist for an elder, create it with status 0.
    Update the task status based on conditions.
    """
    # Get the current year and week number
    today = datetime.today()
    year, week_number = today.isocalendar()[:2]

    # Delegate to the get_weekly_tasks function
    return get_weekly_tasks(year=year, week_number=week_number, db=db)