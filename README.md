## Overview:
The Valorant Esports Analytics Platform is a comprehensive tool designed to analyze player performance data for professional and semi-professional Valorant players. This project scrapes player statistics from platforms like VLR.gg, processes the data, and provides detailed analytics on individual and team performance. Using this data, the platform generates key performance indicators (KPIs) such as K/D ratio, ACS (Average Combat Score), MVP count, and more, ultimately calculating an overall Impact Score for each player.

The platform allows esports teams, coaches, and analysts to:

Track player performance over time and across matches.
Compare player statistics to identify top performers by specific metrics.
Analyze optimal team compositions based on player roles and impact scores.
Visualize data trends and insights to make informed decisions during competitive matches.
The system also integrates with AWS for scalable data storage, analytics, and querying, while providing the ability to store and retrieve large datasets efficiently. Future plans include real-time data integration, advanced machine learning models for predictive performance, and enhanced visual reporting.

## Technology Stack:

Data Scraping: BeautifulSoup, Requests
Data Analytics: Python (Pandas, NumPy, Scikit-learn)
AWS Integration: S3, Bedrock
Visualization: Matplotlib
Security: Secure role-based access and S3 bucket encryption
The production key will enable deeper integration with official Valorant data, allowing for a richer dataset, improving accuracy, and enhancing the platform's value to the Valorant esports community.
