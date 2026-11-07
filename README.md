# 🏥 Pharmacy Expiry Management & Demand Forecasting System

> **An enterprise-grade, end-to-end data analytics and predictive machine learning portfolio project designed to minimize pharmaceutical write-off losses, detect near-expiry stock bottlenecks, and automate targeted clearance markdowns before medicines expire.**

---

# Pharmacy Expiry Management: End-to-End Analytics, Demand Forecasting & Inventory Optimization

## 1. Executive Summary & Business Problem

In retail and clinical pharmacy supply chains, pharmaceutical inventory represents both the primary revenue engine and a substantial financial vulnerability. Inventory mismanagement generates severe operational friction at two opposite extremes: stockouts compromise patient health and forfeit sales revenue, whereas uncalibrated overstocking leads to irreversible inventory decay. Because pharmaceutical items possess legally mandated expiration thresholds, unsold stock cannot remain indefinitely on warehouse shelves; upon expiration, product value depreciates to zero and mandates total financial write-offs alongside specialized disposal costs.

This project delivers an end-to-end analytics engineering, machine learning, and business intelligence solution designed to mitigate write-off losses across pharmaceutical product lines. Standard operational approaches rely on static calendar audits (such as manual reviews identifying items within thirty days of expiration), which introduce critical systemic blind spots:

1. **Unnecessary Margin Cannibalization**: High-velocity essential medications nearing expiration are frequently subjected to panic discounting, forfeiting gross profit on units that would have sold out naturally at full retail price.
2. **Invisible Expiry Accumulation**: Low-velocity, specialized medications expiring beyond standard review windows (for example, sixty to ninety days out) remain unflagged until their remaining shelf-life is shorter than the time required for normal customer demand to clear them.
3. **Decoupled Replenishment**: Procurement orders are placed without reconciling incoming batch volumes against remaining batch shelf-life and empirical sales velocity.

By linking granular transaction history, batch-level shelf-life tracking, and count-regression demand forecasting, this system transforms raw enterprise resource planning data into prescriptive operational interventions, automating promotional markdown triggers to recover capital before expiration occurs.

---

## 2. Quantified Business Impact & Core Financial Findings

Analysis of the enterprise inventory records reveals substantial financial exposure and demonstrates the direct capital preservation achieved through data-driven intervention:

* **Total Portfolio Capitalization**: The master inventory represents **\$665,441.35** in total wholesale acquisition cost across 193 tracked batches, corresponding to an expected gross retail yield of **\$1,105,784.57** (a 66.2% overall portfolio markup).
* **Historical Sunk Cost Write-Offs**: Pre-existing expired inventory accounts for **\$59,041.69** in wholesale acquisition cost (**\$95,620.51** in forfeited retail value) across 77 dormant batches, representing unrecoverable capital.
* **Immediate Critical Exposure**: Active inventory expiring within a 30-day operational window constitutes **\$22,345.52** in near-term wholesale exposure across 10 batches.
* **Near-Term Exposure (31 to 60 Days)**: Stock expiring between 31 and 60 days represents **\$19,392.91** in wholesale value.
* **Therapeutic Risk Concentration**: Imminent waste risk is heavily concentrated in specific clinical categories. **Vitamins & Supplements** leads with **\$13,233.78** in flagged impending waste, followed by **Cardiovascular** (**\$8,664.53**), **Pain Relief & Anti-inflammatory** (**\$6,377.50**), and **Gastrointestinal** (**\$3,334.72**).
* **Storage Condition Liability**: Room-temperature inventory accounts for **\$49,831.20** (84.4%) of all expired capital, whereas refrigerated cold storage accounts for **\$9,210.49**, indicating that standard shelf management requires more rigorous stock rotation than cold-chain logistics.
* **Prescriptive Capital Recovery**: Applying predictive demand modeling isolates exactly **10 batches** exhibiting true surplus stock (where on-hand volume exceeds forecasted 30-day demand), quantifying **\$16,424.81** in predicted wholesale write-offs. Executing automated **35% clearance markdowns** recovers an estimated **\$10,700.00** in liquid capital, directly preventing complete write-offs.

---

## 3. System Architecture & Repository Structure

The project architecture connects data generation, feature engineering, statistical machine learning, and multi-page business intelligence. The physical file organization aligns directly with project directory assets:

```text
PHARMACY-EXPIRY-MANAGEMENT/
├── data/
│   ├── pharmacy_products.csv             # Product dimension (pricing, lead times, reorder levels)
│   ├── pharmacy_inventory_batches.csv    # Inventory fact (batch IDs, dates, stock, storage types)
│   ├── pharmacy_sales_transactions.csv   # Historical sales log (transaction timestamps, units, discounts)
│   ├── cleaned_master_inventory.csv      # Enriched master dataset (velocity, shelf-life, waste flags)
│   └── ml_forecast_expiry_risk.csv       # Model output (forecasts, surplus units, markdown actions)
│
├── notebooks/
│   ├── PHARMACY EXPIRY MANAGEMENT.ipynb       # Phase 1: Ingestion, schema joins, velocity metrics
│   ├── PHARMACY EXPIRY MANAGEMENT EDA.ipynb   # Phase 2: Statistical exploration & 10 business analyses
│   └── PHARMACY EXPIRY MANAGEMENT MODEL.ipynb # Phase 3: Poisson count regression & operational audit
│
├── dashboards/
│   └── Pharmacy_Operations_Executive.pbix     # Phase 4: 4-Page interactive Power BI report
│
├── assets/
│   ├── page0_general_dashboard.png            # UI Architecture: Commercial Performance
│   ├── page1_executive_overview.png           # UI Architecture: Expiry Risk Overview
│   ├── page2_velocity_matrix.png              # UI Architecture: Operational Velocity Matrix
│   ├── page3_ml_action_center.png             # UI Architecture: ML Markdown Action Center
│   └── dashboard_icon_set.png                 # Navigation and KPI icon assets
│
└── README.md                                  # Repository documentation & portfolio briefing
```

### Relational Schema Blueprint

The data model operates on normalized relational tables integrated through primary and foreign keys:

$$\text{pharmacy\_products} \xrightarrow[\text{1 : Many}]{\text{product\_id}} \text{pharmacy\_inventory\_batches} \xrightarrow[\text{1 : 1}]{\text{batch\_id}} \text{ml\_forecast\_expiry\_risk}$$

$$\text{pharmacy\_inventory\_batches} \xrightarrow[\text{1 : Many}]{\text{batch\_id}} \text{pharmacy\_sales\_transactions}$$

$$\text{DimDate} \xrightarrow[\text{1 : Many}]{\text{Date}} \text{pharmacy\_inventory\_batches [expiry\_date]}$$

$$\text{DimDate} \xrightarrow[\text{1 : Many}]{\text{Date}} \text{pharmacy\_sales\_transactions [transaction\_date]}$$

---

## 4. Phase-by-Phase Technical Implementation

### Phase 1: Data Engineering & Feature Architecture

Raw retail datasets frequently omit non-transactional dates and isolate batch lifespans from sales records. The data pipeline standardizes timestamps, establishes fixed evaluation anchors, and constructs critical operational metrics:

1. **Temporal Anchoring**: A static temporal anchor of `2026-10-26` is established across all calculations to ensure deterministic evaluation. Remaining shelf-life is calculated as:
   $$\text{days\_to\_expiry} = \text{expiry\_date} - \text{analysis\_date}$$
2. **Expiry Risk Stratification**: Batches are grouped into risk tiers using vectorized conditional logic:
   * *Expired*: $\text{days\_to\_expiry} < 0$
   * *Critical Risk*: $0 \le \text{days\_to\_expiry} \le 30$
   * *High Risk*: $31 \le \text{days\_to\_expiry} \le 60$
   * *Moderate Risk*: $61 \le \text{days\_to\_expiry} \le 90$
   * *Fresh Stock*: $\text{days\_to\_expiry} > 90$
3. **90-Day Rolling Sales Velocity**: Historical transaction logs are sliced over the preceding 90 days to derive normalized daily run-rates:
   $$\text{avg\_daily\_sales} = \frac{\sum_{t \in T_{90}} \text{units\_sold}_t}{90}$$
4. **Run-Rate Depletion Time**: Expected days required to exhaust on-hand inventory is computed via guarded vector division:
   $$\text{days\_of\_stock\_remaining} = \begin{cases} \frac{\text{current\_stock\_quantity}}{\text{avg\_daily\_sales}}, & \text{if } \text{avg\_daily\_sales} > 0 \\ 9999, & \text{otherwise} \end{cases}$$
5. **Deterministic Waste Boundary Flagging**: A binary flag isolates inventory that will mathematically expire before consumer demand exhausts it:
   $$\text{waste\_risk\_flag} = (\text{days\_to\_expiry} > 0) \land (\text{days\_to\_expiry} \le 90) \land (\text{days\_of\_stock\_remaining} > \text{days\_to\_expiry})$$

---

### Phase 2: Exploratory Data Analysis & Strategic Insights

Statistical examination across operational dimensions resolved ten primary business inquiries:

| Strategic Business Question | Analytical Methodology | Concrete Finding | Operational Significance |
| :--- | :--- | :--- | :--- |
| **Capital Exposure by Expiry Tier** | Aggregation of wholesale value grouped by expiry status | **\$59,041.69** expired; **\$22,345.52** in critical 0–30d window; **\$19,392.91** in 31–60d window. | Quantifies sunk capital write-offs versus capital requiring active mitigation. |
| **Category Waste Concentration** | Summation of wholesale cost where `waste_risk_flag = True` | **Vitamins & Supplements** (**\$13.2K**) and **Cardiovascular** (**\$8.7K**) dominate risk. | Focuses promotional campaigns on categories yielding the highest cash recovery. |
| **Stagnant Overstocked Stock** | Filtering unexpired stock with $\text{days\_of\_stock\_remaining} > 180$ | Exactly **9 unexpired product batches** hold over 6 months of supply. | Informs immediate procurement freezes on overstocked SKUs. |
| **Gross Margin vs. Waste Risk** | Profit margin distribution comparison across waste flag states | Flagged waste batches average **42.86%** margin versus **38.76%** for safe inventory. | Confirms write-offs disproportionately erode high-margin product lines. |
| **Storage Condition Liability** | Two-way cross-tabulation of storage type and expiry tiers | Room temperature stock accounts for **\$49,831.20** (84.4%) of expired wholesale loss. | Demonstrates that standard shelving requires stricter FEFO compliance than cold chain. |
| **Top SKU Retail Liability** | Retail valuation ranking of batches expiring within 60 days | Top liabilities: Vitamin C 500mg (**\$15.5K**), Atorvastatin (**\$14.4K**), Losartan (**\$12.7K**). | Provides floor staff with an itemized target list for prescribers and markdowns. |
| **Supplier Lead Time Impact** | Kernel density estimation of lead times across waste states | Flagged waste batches average shorter lead times (**6.78d**) than safe stock (**10.37d**). | Proves supplier delivery delay is not the primary cause of waste; excess batch order volume is. |
| **Replenishment Compliance** | Boolean threshold audit ($\text{stock} < \text{reorder\_level}$) | **115 of 193 batches (59.6%)** operate below assigned reorder points. | Highlights stockout vulnerabilities occurring simultaneously alongside expiry waste. |
| **Portfolio Markup Potential** | Cost valuation versus gross retail yield comparison | Wholesale capital of **\$665.4K** holds an expected retail value of **\$1.11M** (66.2% markup). | Sets the maximum achievable financial baseline under zero-waste operations. |
| **Velocity Risk Boundary ($y=x$)** | Scatter plot of $\text{days\_to\_expiry}$ vs $\text{days\_of\_stock\_remaining}$ | Batches above the diagonal $y = x$ boundary cannot clear prior to expiration. | Visual proof separating healthy stock from impending inventory write-offs. |

---

### Phase 3: Machine Learning Demand Forecasting & Prescriptive Audit

#### Algorithmic Formulation & Architectural Evolution

Forecasting pharmaceutical demand at the stock-keeping-unit level introduces severe zero-inflation and intermittent volatility. The modeling pipeline underwent systematic architectural refinement:

* **Initial Daily Regression Baseline**: Initial models (Ridge Regression, Random Forest, Gradient Boosting) attempted to predict exact daily unit sales per product. This formulation produced low predictive power ($R^2$ scores between $0.071$ and $0.092$, MAE of $\approx 3.2$ units/day). Standard regressors treated discrete integer counts as continuous Gaussian variables and suffered from daily noise.
* **Log-Transformation Instability**: Applying log transformations ($\ln(1 + y)$) with Mean Squared Error loss resulted in negative $R^2$ scores ($-0.023$ to $-0.038$) upon re-exponentiation ($\exp(\hat{y}) - 1$). Slight over-predictions on zero-sales days were exponentially inflated, heavily penalizing squared-error metrics.
* **Weekly Aggregation & Poisson Objective**: Transitioning from daily sales to **7-day weekly totals** aligned the forecast with actual pharmacy replenishment intervals, filtering out daily purchasing noise. The final production architecture deployed **Histogram-Based Gradient Boosting (`HistGradientBoostingRegressor`) with a Poisson loss function (`loss='poisson'`)**:

$$\mathcal{L}(y, \hat{y}) = \sum_{i} \left( \hat{y}_i - y_i \ln(\hat{y}_i) \right)$$

#### Feature Engineering Pipeline

To prevent temporal look-ahead bias, feature engineering applied strict chronological shifting:
* **Historical Autoregressive Lags**: Weekly lags (`lag_1w`, `lag_2w`) captured weekly demand momentum.
* **Rolling Moving Averages**: 4-week rolling means (`rolling_mean_4w`) smoothed mid-term trends.
* **Product Target Encoding**: Historical product baseline means (`product_hist_weekly_mean`) were computed strictly within the training set and mapped into validation partitions to provide individual SKU velocity anchors.
* **Calendar Seasonality**: Month-of-year indicators accounted for annual seasonal fluctuations.

#### Chronological Validation & Model Performance

The dataset was split chronologically, training on historical records and testing on the final 8 weeks of unseen data:

| Model Architecture | Target Formulation | MAE (Weekly Units) | RMSE (Weekly Units) | $R^2$ Score | Operational Viability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ridge Regression (Baseline)** | Daily Sales | 2.848 units/day | 4.416 units/day | -0.038 | Inadequate; high outlier penalties |
| **Random Forest Regressor** | Daily Sales (Log) | 3.160 units/day | 4.180 units/day | -0.025 | Inadequate; variance distortion |
| **HistGradientBoosting (Daily)** | Daily Count (Poisson) | 1.434 units/day | 1.828 units/day | 0.084 | Baseline count model |
| **HistGradientBoosting (Weekly)** | **Weekly Count (Poisson)** | **9.426 units/week** | **12.132 units/week** | **0.190** | **Production standard; +126% fit improvement** |

An MAE of **9.426 units per week** corresponds to a daily-equivalent error of $\pm 1.35$ units per product, providing an accurate basis for operational planning. Feature importance, evaluated via `permutation_importance` on test data, confirmed that baseline velocity (`product_hist_weekly_mean`), recent momentum (`lag_1w`), and calendar month dominate predictive influence.

#### Prescriptive Audit Engine

Weekly forecasts were scaled to a 30-day window ($\hat{Y}_{30\text{d}} = \hat{Y}_{\text{weekly}} \times \frac{30}{7}$) and integrated with inventory records expiring within 30 days:
$$\text{expected\_expired\_units} = \max\left(0, \;\text{current\_stock\_quantity} - \hat{Y}_{30\text{d}}\right)$$
$$\text{predicted\_financial\_waste\_usd} = \text{expected\_expired\_units} \times \text{unit\_cost\_usd}$$

The system automatically generates operational directives: batches exhibiting positive surplus are assigned `'TRIGGER IMMEDIATE 30-40% CLEARANCE MARKDOWN'`, whereas batches projected to sell out naturally are assigned `'MAINTAIN FULL RETAIL PRICE'`.

---

### Phase 4: Enterprise Power BI Multi-Page Dashboard

The analytical results are deployed in a 4-page interactive Power BI application structured around executive oversight and operational execution.

#### Data Model & Star Schema Architecture
* **`DimDate` Dimension**: Generated via DAX `CALENDAR()`, marked as an official Date Table, and linked to `cleaned_master_inventory[expiry_date]` and `pharmacy_sales_transactions[transaction_date]`.
* **Fact Tables**: `cleaned_master_inventory` (batch-level inventory state), `ml_forecast_expiry_risk` (prescriptive model outputs), and `pharmacy_sales_transactions` (granular sales logs).
* **Cardinality**: `cleaned_master_inventory` connects $1 : 1$ (bidirectional cross-filter) to `ml_forecast_expiry_risk`, and $1 : \text{Many}$ (single cross-filter) to `pharmacy_sales_transactions`.

#### Core DAX Business Logic

```dax
// 1. Commercial Valuation
Total Wholesale Stock Value = SUM(cleaned_master_inventory[stock_value_cost_usd])
Total Retail Stock Value = SUM(cleaned_master_inventory[stock_value_retail_usd])
Total Potential Gross Margin = [Total Retail Stock Value] - [Total Wholesale Stock Value]

// 2. Risk & Write-Off Exposure
Already Expired Cost Loss = 
CALCULATE([Total Wholesale Stock Value], cleaned_master_inventory[days_to_expiry] < 0)

Critical Risk Cost (0-30 Days) = 
CALCULATE([Total Wholesale Stock Value], cleaned_master_inventory[days_to_expiry] >= 0, cleaned_master_inventory[days_to_expiry] <= 30)

Near Expiry Exposure (0-60 Days) = 
CALCULATE([Total Wholesale Stock Value], cleaned_master_inventory[days_to_expiry] >= 0, cleaned_master_inventory[days_to_expiry] <= 60)

Portfolio Waste Exposure % = DIVIDE([Near Expiry Exposure (0-60 Days)], [Total Wholesale Stock Value], 0)

// 3. Prescriptive ML Integration & Capital Recovery
ML Predicted Financial Waste = SUM(ml_forecast_expiry_risk[predicted_financial_waste_usd])

Batches Requiring Markdown Action = 
CALCULATE(DISTINCTCOUNT(ml_forecast_expiry_risk[batch_id]), ml_forecast_expiry_risk[expected_expired_units] > 0)

Projected Clearance Recovery Revenue = 
SUMX(
    ml_forecast_expiry_risk,
    ml_forecast_expiry_risk[expected_expired_units] * RELATED(cleaned_master_inventory[selling_price_usd]) * 0.65
)
```

#### Page Layouts & User Experience

Four dedicated dashboard views establish complete operational visibility:
1. **Commercial Performance (Page 1)**: Tracks macro sales health, gross profit margins across product lines, top-selling medications, and inventory turnover efficiency.
2. **Executive Expiry Risk Overview (Page 2)**: Visualizes portfolio capital exposure, monitoring the \$59.0K sunk cost loss and mapping imminent risk concentration across clinical drug categories.
3. **Operational Velocity Matrix (Page 3)**: Features the Velocity Risk Boundary scatter plot ($y = x$), isolating batches in the danger zone alongside a batch-level detail matrix with automated risk status highlights.
4. **ML Prescriptive Clearance Center (Page 4)**: Compares on-hand batch volume against 30-day Poisson forecasts, translating predicted surplus into actionable clearance markdown directives.

---

## 5. Recruiter & Interview Presentation Walkthrough

When presenting this project during technical screenings, portfolio reviews, or case study interviews, follow this structured communication framework:

### 1. The Elevator Pitch (30 Seconds)
> "I developed an end-to-end Pharmacy Expiry Management system that combines data engineering, machine learning demand forecasting, and an executive Power BI dashboard to solve pharmaceutical inventory decay. Rather than relying on basic static expiry alerts that either discount fast-selling drugs needlessly or miss slow-moving items entirely, I built a Poisson count-regression model that identifies exactly where batch stock surpasses 30-day forecasted demand. Across our test portfolio, this identified \$16.4K in guaranteed surplus waste and automated markdown rules to recover over \$10K in liquid capital before expiration."

### 2. Discussing the Data Pipeline & Engineering Choices
* **Real-World Relational Thinking**: Explain that real enterprise systems do not provide flat spreadsheets. Emphasize how you joined normalized product dimensions, inventory batch facts, and transactional receipt logs.
* **Guarded Metrics**: Highlight data engineering details such as filling non-transactional dates with zero sales before calculating moving averages, and handling zero-sales divisions when computing run-rate duration.

### 3. Defending Machine Learning Decisions
* **Why Not Standard Random Forest / Linear Regression?**: State clearly that daily pharmaceutical demand consists of non-negative count integers ($0, 1, 2, 3\dots$) with heavy zero-inflation. Linear regression predicts impossible negative sales, while log-transformed models distort variance upon exponentiation.
* **The Weekly Aggregation Pivot**: Explain the architectural decision to aggregate daily sales to weekly intervals. This smoothed daily noise, increased the model $R^2$ fit by 126%, and aligned forecasting directly with weekly pharmacy replenishment cycles.
* **Leakage Prevention**: Highlight that historical rolling averages used chronological shifting (`.shift(1)`), train/test splits were conducted chronologically rather than randomly, and product target encodings were calculated strictly within training sets.

### 4. Demonstrating Business Intelligence & Executive Impact
* **Star Schema Over Flat Tables**: Point out that the Power BI report uses an active Date Dimension with one-to-many relationships, optimizing memory efficiency and cross-filtering performance.
* **Prescriptive Over Descriptive**: Emphasize that the dashboard avoids passive data reporting. Page 4 functions as an operational decision engine, providing floor staff with a daily list of specific batch IDs requiring promotional clearance pricing to maximize capital recovery.


---

## 6. How to Run & Reproduce This Project

### 6.1 Prerequisites
* Python 3.10+ (with , , , , )
* Jupyter Notebook or JupyterLab
* Microsoft Power BI Desktop (for the multi-page  dashboard)

### 6.2 Setup & Execution
1. **Clone or Download the Repository**:
   Download the repository zip or clone it into your local workspace.
2. **Install Dependencies**:
   Ensure required data science packages are installed in your Python environment:
   Requirement already satisfied: pandas in /usr/local/lib/python3.12/site-packages (2.2.3)
Requirement already satisfied: numpy in /usr/local/lib/python3.12/site-packages (2.4.3)
Requirement already satisfied: scikit-learn in /usr/local/lib/python3.12/site-packages (1.8.0)
Requirement already satisfied: matplotlib in /usr/local/lib/python3.12/site-packages (3.10.8)
Requirement already satisfied: seaborn in /usr/local/lib/python3.12/site-packages (0.13.2)
Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/site-packages (from pandas) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/site-packages (from pandas) (2026.3.post1)
Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/site-packages (from pandas) (2026.3)
Requirement already satisfied: scipy>=1.10.0 in /usr/local/lib/python3.12/site-packages (from scikit-learn) (1.17.1)
Requirement already satisfied: joblib>=1.3.0 in /usr/local/lib/python3.12/site-packages (from scikit-learn) (1.5.3)
Requirement already satisfied: threadpoolctl>=3.2.0 in /usr/local/lib/python3.12/site-packages (from scikit-learn) (3.6.0)
Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.12/site-packages (from matplotlib) (1.3.3)
Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.12/site-packages (from matplotlib) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.12/site-packages (from matplotlib) (4.63.0)
Requirement already satisfied: kiwisolver>=1.3.1 in /usr/local/lib/python3.12/site-packages (from matplotlib) (1.5.0)
Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.12/site-packages (from matplotlib) (26.3)
Requirement already satisfied: pillow>=8 in /usr/local/lib/python3.12/site-packages (from matplotlib) (11.3.0)
Requirement already satisfied: pyparsing>=3 in /usr/local/lib/python3.12/site-packages (from matplotlib) (3.3.2)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)
3. **Run the Notebooks in Order**:
   - : Ingests raw CSVs, merges relational entities, and engineers expiry risk and sales velocity metrics.
   - : Visualizes inventory distributions, therapeutic category liabilities, and velocity parity boundaries.
   - : Aggregates transactions into 7-day buckets, trains the Poisson gradient boosting regressor, and exports prescriptive markdown decision tables.
4. **Open the Power BI Dashboard**:
   Open  in Power BI Desktop to interact with the 4-page executive report.

---

## 7. License

This project is licensed under the MIT License - open-source for learning, demonstration, and enterprise decision-support benchmarking.
