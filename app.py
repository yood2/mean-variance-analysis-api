from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from hermes import ModernPortfolio

app = Flask(__name__)
api = Api(app)

class PortfolioResource(Resource):
    def get(self):
        tickers = request.args.get('tickers')
        start_date = request.args.get('start_date', '2018-01-01')
        end_date = request.args.get('end_date', '2024-01-01')

        if not tickers:
            return {'message': 'No tickers provided'}, 400
        
        tickers_list = tickers.split(',')

        try:
            portfolio = ModernPortfolio(tickers_list, start_date, end_date)
            optimal_weights = portfolio.optimize_portfolio()
            return jsonify({'optimal_weights': optimal_weights})
        
        except Exception as e:
            return {'message': str(e)}, 500

api.add_resource(PortfolioResource, '/portfolio')

if __name__ == '__main__':
    app.run(debug=True)