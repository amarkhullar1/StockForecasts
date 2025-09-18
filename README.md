# Stock Forecast App

A Django web application that enables analysts to input and manage their forecasts for stocks within their coverage universe.

## Features

- **Forecast Submission**: Analysts can submit forecasts for 1 month, 3 months, and 12 months periods
- **EPS Predictions**: Forecasts include predicted earnings per share (EPS) values (positive or negative)
- **Full History**: All forecast updates are preserved with timestamps
- **Search Functionality**: Search tickers by name or symbol
- **Admin Interface**: Full Django admin interface for management

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Import tickers from universe.csv**:
   ```bash
   python manage.py import_tickers
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   
   **Set admin password** (if created without password):
   ```bash
   python set_admin_password.py
   ```
   
   **Make admin a staff member** (for forecast history access):
   ```bash
   python make_admin_staff.py
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - Forecast History (Admin): http://127.0.0.1:8000/forecast/history/

## Usage

### For Analysts

1. **View Tickers**: Visit the main page to see all available tickers
2. **Search**: Use the search box to find specific tickers
3. **Submit Forecasts**: Click "Add/Update" next to any ticker/period to submit a forecast
4. **Forecast Details**: 
   - Enter the predicted EPS (earnings per share)
   - Add optional detailed view/notes
   - Select the forecast period (1M, 3M, or 12M)

### For Administrators

1. **Admin Access**: Use the superuser account to access http://127.0.0.1:8000/admin/
2. **Forecast History**: Access detailed forecast history with filtering at http://127.0.0.1:8000/forecast/history/
3. **Manage Tickers**: Add, edit, or remove tickers from the coverage universe
4. **View All Forecasts**: See all forecast submissions with full history
5. **User Management**: Manage analyst accounts and permissions

## Data Structure

### Ticker Model
- `ticker`: Stock symbol (e.g., AAPL)
- `name`: Company name (e.g., Apple Inc.)

### Forecast Model
- `ticker`: Foreign key to Ticker
- `analyst`: Foreign key to User (analyst who made the forecast)
- `period`: Forecast period (1M, 3M, 12M)
- `direction`: Predicted EPS value (float, can be positive or negative)
- `view`: Optional detailed analysis/notes
- `is_current`: Boolean indicating if this is the latest forecast
- `submitted_at`: Timestamp when forecast was created
- `updated_at`: Timestamp when forecast was last modified

## Forecast History

- Each forecast submission creates a new record (immutable)
- Previous forecasts for the same (analyst, ticker, period) are marked as historic (`is_current=False`)
- Full history is preserved with timestamps
- Only the most recent forecast per (analyst, ticker, period) is displayed as current

## Universe.csv Format

The `universe.csv` file should contain:
```csv
ticker,name
AAPL,Apple Inc.
MSFT,Microsoft Corporation
...
```

## Customization

### Adding New Tickers
1. Update `universe.csv` with new tickers
2. Run `python manage.py import_tickers`

### Modifying Forecast Periods
Edit the `PERIOD_CHOICES` in `forecasts/models.py`

### Styling
Modify the CSS in the template files:
- `forecasts/templates/forecasts/ticker_list.html`
- `forecasts/templates/forecasts/forecast_form.html`

## Technical Details

- **Framework**: Django 4.2.23
- **Database**: SQLite (default)
- **Authentication**: Django's built-in user authentication
- **Templates**: Custom Django templates with CSS styling
- **Management Commands**: Custom command for importing tickers

## Security Notes

- Change the `SECRET_KEY` in `stock_forecast_app/settings.py` for production
- Set `DEBUG = False` for production
- Configure proper database settings for production
- Use HTTPS in production
- Implement proper user authentication and authorization

## Troubleshooting

### Common Issues

1. **"No module named 'stock_forecast_app'"**: Ensure you're in the correct directory and the project structure is correct
2. **Migration errors**: Delete the database file and run migrations again
3. **Template errors**: Check that all template files are in the correct locations
4. **Import errors**: Ensure all dependencies are installed

### Getting Help

- Check Django documentation: https://docs.djangoproject.com/
- Review the Django tutorial: https://docs.djangoproject.com/en/4.2/intro/tutorial01/ 