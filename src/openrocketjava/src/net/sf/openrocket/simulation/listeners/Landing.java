package net.sf.openrocket.simulation.listeners;

import net.sf.openrocket.simulation.*;
import net.sf.openrocket.simulation.exception.SimulationException;
import net.sf.openrocket.simulation.listeners.AbstractSimulationListener;
import net.sf.openrocket.util.GeodeticComputationStrategy;
import net.sf.openrocket.util.WorldCoordinate;


public class Landing extends AbstractSimulationListener {

	@Override
	public void endSimulation(SimulationStatus status, SimulationException exception) {
		WorldCoordinate c = status.getRocketWorldPosition();
		SimulationConditions conditions = status.getSimulationConditions();
		WorldCoordinate site = conditions.getLaunchSite();
		GeodeticComputationStrategy comp = conditions.getGeodeticComputation();

		WorldCoordinate range = comp.addCoordinate(site,status.getRocketPosition());
		System.out.println("New landing: "  + range);
	}


}
