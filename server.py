from flask import Flask, render_template
import mergeLogic as ml
q_or_rev = ml.statement_analyzer("i want a saree for onam")
